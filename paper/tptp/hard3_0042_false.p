% hard3_0042  eq1=258 eq2=851  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(f(X,X),Y),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(X,f(f(Y,Y),f(Z,W))) )).
