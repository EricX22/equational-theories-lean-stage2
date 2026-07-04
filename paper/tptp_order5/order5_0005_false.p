% order5_0005  eq1=37731 eq2=4884  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,f(Z,f(Y,X))),Y),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(Y,f(Z,f(W,f(Z,Z))))) )).
