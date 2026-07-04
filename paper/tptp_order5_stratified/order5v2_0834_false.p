% order5v2_0834  eq1=38319 eq2=2865  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,f(f(X,Z),Y)),Y),X) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(X,f(Y,X)),Y),X) )).
