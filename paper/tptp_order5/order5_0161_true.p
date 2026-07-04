% order5_0161  eq1=53755 eq2=52377  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(f(Z,W),W),Z),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(X,f(Z,Z)),W),Y) )).
