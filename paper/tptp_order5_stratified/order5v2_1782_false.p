% order5v2_1782  eq1=7957 eq2=50361  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(f(Y,f(Z,W)),W))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( f(X,X) != f(f(Y,f(f(X,Y),X)),X) )).
