% order5v2_1182  eq1=38464 eq2=58264  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(f(Y,Z),X)),W),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(f(X,X),Y) != f(X,f(Z,f(X,X))) )).
