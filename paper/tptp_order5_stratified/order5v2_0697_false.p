% order5v2_0697  eq1=26869 eq2=1459  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,X),f(Y,X)),f(Z,W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,Y),f(Y,f(Z,Z))) )).
