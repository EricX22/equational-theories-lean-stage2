% order5_0049  eq1=6217 eq2=23275  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(Y,f(f(W,Z),Z)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(X,Y),Z),f(Z,f(X,W))) )).
