% order5_0101  eq1=28912 eq2=62535  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,Z),X),Y),f(W,U)) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( f(f(X,Y),Z) != f(f(f(W,W),U),Y) )).
