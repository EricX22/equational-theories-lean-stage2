% order5_0063  eq1=51733 eq2=468  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(Z,X),f(W,X)),Y) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(X,f(X,f(Y,Z)))) )).
