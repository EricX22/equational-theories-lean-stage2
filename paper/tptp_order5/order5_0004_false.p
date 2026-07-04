% order5_0004  eq1=9815 eq2=7807  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,V,W,X,Y,Z] : ( X = f(Y,f(f(Z,Z),f(W,f(U,V)))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Y,f(f(Z,f(W,X)),Z))) )).
