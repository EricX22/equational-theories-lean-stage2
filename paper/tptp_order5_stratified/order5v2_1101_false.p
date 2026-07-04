% order5v2_1101  eq1=11233 eq2=62056  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(Y,f(Y,X)),f(Z,Z))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( f(f(X,Y),Y) != f(f(f(X,X),X),Z) )).
