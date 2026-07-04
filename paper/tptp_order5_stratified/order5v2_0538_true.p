% order5v2_0538  eq1=18203 eq2=37954  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,V,W,X,Y,Z] : ( X = f(f(Y,X),f(Z,f(f(W,U),V))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(f(Y,f(Z,f(W,Z))),U),Z) )).
