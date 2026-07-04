% order5v2_0732  eq1=4969 eq2=38683  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(X,f(Y,f(Z,f(W,Z))))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(Y,f(f(Z,Z),X)),X),W) )).
