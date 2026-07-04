% order5_0113  eq1=62023 eq2=58680  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(f(X,Y),X) = f(f(f(Z,Z),W),X) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(f(X,Y),Y) != f(Z,f(W,f(Y,U))) )).
